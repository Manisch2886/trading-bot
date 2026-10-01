#!/usr/bin/env python3
"""TB-126 A6: Ueberschriften gegen Anhang A Tabelle 1, Marken gegen Anhang A Tabelle 2 (Daten-Block),
Abschnitt 10 und ERZEUGT-Block gegen die Belege aus 0d.

Unabhaengig vom Einsetzskript. Ueberschriften aus der Markdown-Tabelle 1 des Auftrags am Commit S0
(nicht aus dem JSON). Je Marke: Markenzeile 1 (⟨DATUM⟩ -> Datum) genau 1-mal im Register, Markenzeile 2
direkt darunter, Leerzeile davor, und die naechste Zeile davor, die keine TB-126-Marke und keine Leerzeile
ist, beginnt wie die Einfuegestelle (anfang40). Die Marke unter 48.16 liegt zwischen dem Zitatblock R48
und der Kette von 48.16. Alle Markenzeilen mit 'TB-126, <Datum>)' gezaehlt: Soll 88.
Aufruf:  trading-env/bin/python3 docs/belege/TB-126/a6_marken.py <S0> <datum> [<register>]
"""
import json
import re
import subprocess
import sys

S0, DATUM = sys.argv[1], sys.argv[2]
REG = sys.argv[3] if len(sys.argv) > 3 else "docs/VORREGISTRIERUNG_neuselektion.md"
BL = "docs/belege/TB-126/"
auf = subprocess.run(["git", "show", "%s:docs/auftraege/MAC_TB-126_register_e2.md" % S0], capture_output=True,
                     text=True, check=True).stdout
daten = json.loads(auf.split("DATEN-ANFANG\n", 1)[1].split("\nDATEN-ENDE", 1)[0])
t1 = auf.split("## Tabelle 1", 1)[1].split("## Tabelle 2", 1)[0]
ueber = [re.split(r"(?<!\\)\|", s)[4].strip().strip("`") for s in t1.split("\n") if re.match(r"^\| 4[789]\.\d+ \|", s)]
text = open(REG, encoding="utf-8").read()
L = text.split("\n")
fehler = []
print("# TB-126 A6 Ueberschriften und Marken: Register %s, Auftrag am Commit %s, Datum %s" % (REG, S0, DATUM))

print("## Ueberschriften (Tabelle 1)")
g = 0
for u in ueber:
    n = L.count(u)
    g += n == 1
    if n != 1:
        fehler.append("Ueberschrift %dx: %s" % (n, u))
print("Ueberschriften: %d/%d genau einmal als ganze Zeile" % (g, len(ueber)))

MARKE = re.compile(r"^> ⭐ \*\*.*TB-126, " + re.escape(DATUM) + r"\)\.$")
M2 = "> Eintrag und Stand oben bleiben zeichengleich."
print("## Marken (Tabelle 2, Daten-Block): gesetzt / nicht gesetzt, Zeile nachher")
gesetzt = 0
for m in daten["marken"]:
    m1 = m["m1"].replace("⟨DATUM⟩", DATUM)
    t = [i for i, s in enumerate(L) if s == m1]
    ok = len(t) == 1
    if ok:
        i = t[0]
        ok = L[i + 1] == M2 and L[i - 1] == ""
        k = i - 1
        while k >= 0 and (L[k] == "" or MARKE.match(L[k]) or (L[k] == M2 and MARKE.match(L[k - 1]))):
            k -= 1
        ok = ok and L[k].startswith(m["anfang40"])
    gesetzt += ok
    print("Nr %2d R%-4s %s Zeile %s" % (m["nr"], m["R"] or "-", "gesetzt" if ok else "NICHT GESETZT/FALSCH",
                                       t[0] + 1 if t else "-"))
    if not ok:
        fehler.append("Marke Nr %d" % m["nr"])
r54 = daten["r54_unter_48_16"]["m1"].replace("⟨DATUM⟩", DATUM)
t = [i for i, s in enumerate(L) if s == r54]
ok54 = False
if len(t) == 1:
    i = t[0]
    a = max(k for k in range(i) if L[k].startswith("### 48.16 "))
    b = next(k for k in range(i, len(L)) if L[k].startswith("**Kette:**"))
    c = next(k for k in range(i, len(L)) if L[k].startswith("### "))
    ok54 = L[i + 1] == M2 and L[i - 1] == "" and L[i - 2].startswith("> ") and b < c and L[b - 1] == "" and b == i + 3
print("Nr 88 R54 (unter 48.16) %s Zeile %s" % ("gesetzt" if ok54 else "NICHT GESETZT/FALSCH", t[0] + 1 if t else "-"))
if not ok54:
    fehler.append("Marke unter 48.16")
alle = sum(1 for s in L if MARKE.match(s))
print("Marken gesetzt: %d am alten Ort + %d unter 48.16; Markenzeilen 'TB-126, %s' im Register: %d (Soll 88)"
      % (gesetzt, int(ok54), DATUM, alle))
if alle != 88:
    fehler.append("Markenzahl %d" % alle)
# Abschnitt 9: genau eine
k9 = next(i for i, s in enumerate(L) if s.startswith("## 9. "))
k10 = next(i for i, s in enumerate(L) if s.startswith("## 10."))
k11 = next(i for i, s in enumerate(L) if s.startswith("## 11."))
n9 = sum(1 for s in L[k9:k10] if MARKE.match(s))
n10 = sum(1 for s in L[k10:k11] if MARKE.match(s))
print("Marken in Abschnitt 9: %d (Soll 1); in Abschnitt 10: %d (Soll 0)" % (n9, n10))
if n9 != 1 or n10:
    fehler.append("Abschnitt 9/10")

print("## Abschnitt 10 und ERZEUGT-Block gegen 0d (inhaltlich bytegleich)")
ea = next(i for i, s in enumerate(L) if s.startswith("<!-- ERZEUGT:"))
ee = next(i for i, s in enumerate(L) if s.startswith("<!-- ENDE ERZEUGT -->"))
a10 = "\n".join(L[k10:k11]) + "\n"
erz = "\n".join(L[ea:ee + 1]) + "\n"
v10 = open(BL + "0d_abschnitt10_vorher.txt", encoding="utf-8").read()
verz = open(BL + "0d_erzeugt_vorher.txt", encoding="utf-8").read()
print("Abschnitt 10: Z. %d-%d, gleich 0d: %s" % (k10 + 1, k11, "ja" if a10 == v10 else "NEIN"))
print("ERZEUGT-Block: Z. %d-%d, gleich 0d: %s" % (ea + 1, ee + 1, "ja" if erz == verz else "NEIN"))
if a10 != v10 or erz != verz:
    fehler.append("Abschnitt 10/ERZEUGT")
if fehler:
    print("ABWEICHUNG:", fehler)
    sys.exit(1)
print("rc 0: alles wie Anhang A")

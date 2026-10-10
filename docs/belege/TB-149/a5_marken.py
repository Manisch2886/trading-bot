#!/usr/bin/env python3
"""TB-149 A5: Ueberschriften und Ketten gegen Anhang A Tabelle 1, Marken gegen Anhang A Tabelle 2
(Daten-Block), Abschnitt 10 und ERZEUGT-Block gegen die Belege aus 0b.

Unabhaengig vom Einsetzskript. Ueberschriften und Ketten aus der Markdown-Tabelle 1 des Auftrags (Spalten Ueberschrift und Kette; Spalte Zeichen uebergangen) am
Commit S0 (nicht aus dem JSON). Je Ueberschrift: genau 1-mal als ganze Zeile; die Kette ist die Zeile nach
der ersten Leerzeile hinter dem Blockzitat. Je Marke: Markenzeile 1 (⟨DATUM⟩ -> Datum) genau 1-mal im
Register, Markenzeile 2 direkt darunter, Leerzeile davor, und die naechste Zeile davor, die keine
TB-149-Marke und keine Leerzeile ist, beginnt wie die Einfuegestelle (anfang40). Alle Markenzeilen mit
'TB-149, <Datum>)' gezaehlt: Soll 31; in Abschnitt 9 und 10 und im ERZEUGT-Block: Soll 0.
Aufruf:  trading-env/bin/python3 docs/belege/TB-149/a5_marken.py <S0> <datum> [<register>]
"""
import json
import re
import subprocess
import sys

S0, DATUM = sys.argv[1], sys.argv[2]
REG = sys.argv[3] if len(sys.argv) > 3 else "docs/VORREGISTRIERUNG_neuselektion.md"
BL = "docs/belege/TB-149/"
auf = subprocess.run(["git", "show", "%s:docs/auftraege/MAC_TB-149_register_fable_09a.md" % S0],
                     capture_output=True, text=True, check=True).stdout
daten = json.loads(auf.split("DATEN-ANFANG\n", 1)[1].split("\nDATEN-ENDE", 1)[0])
t1 = auf.split("### Tabelle 1", 1)[1].split("### Tabelle 2", 1)[0]
zeilen_t1 = [re.split(r"(?<!\\)\|", s) for s in t1.split("\n") if re.match(r"^\| 56\.\d \|", s)]
ueber = [(sp[2].strip().strip("`"), sp[4].strip().strip("`")) for sp in zeilen_t1]   # Spalte 3 = Zeichen
text = open(REG, encoding="utf-8").read()
L = text.split("\n")
fehler = []
print("# TB-149 A5 Ueberschriften, Ketten und Marken: Register %s, Auftrag am Commit %s, Datum %s" % (REG, S0, DATUM))

print("## Ueberschriften und Ketten (Tabelle 1)")
gu = gk = 0
for u, kette in ueber:
    t = [i for i, s in enumerate(L) if s == u]
    ok_u = len(t) == 1
    ok_k = False
    if ok_u:
        k = t[0] + 2
        while L[k] != "":
            k += 1
        ok_k = L[k + 1] == kette
    gu += ok_u
    gk += ok_k
    print("%s: Ueberschrift %s, Kette %s" % (u[4:8], "gleich" if ok_u else "NEIN", "gleich" if ok_k else "NEIN"))
    if not (ok_u and ok_k):
        fehler.append("Ueberschrift/Kette %s" % u[:12])
print("Ueberschriften: %d/%d, Ketten: %d/%d gleich" % (gu, len(ueber), gk, len(ueber)))
if len(ueber) != 6:
    fehler.append("Tabelle 1 hat %d Zeilen" % len(ueber))

MARKE = re.compile(r"^> ⭐ \*\*.*TB-149, " + re.escape(DATUM) + r"\)\.$")
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
    print("Nr %2d R%-3s %-28s %s Zeile %s" % (m["nr"], m["R"], m["stelle"], "gesetzt" if ok else "NICHT GESETZT/FALSCH",
                                            t[0] + 1 if t else "-"))
    if not ok:
        fehler.append("Marke Nr %d" % m["nr"])
alle = sum(1 for s in L if MARKE.match(s))
print("Marken gesetzt: %d/31; Markenzeilen 'TB-149, %s' im Register: %d (Soll 31)" % (gesetzt, DATUM, alle))
if alle != 31 or gesetzt != 31:
    fehler.append("Markenzahl %d/%d" % (gesetzt, alle))
k9 = next(i for i, s in enumerate(L) if s.startswith("## 9."))
k10 = next(i for i, s in enumerate(L) if s.startswith("## 10."))
k11 = next(i for i, s in enumerate(L) if s.startswith("## 11."))
ea = next(i for i, s in enumerate(L) if s.startswith("<!-- ERZEUGT:"))
ee = next(i for i, s in enumerate(L) if s.startswith("<!-- ENDE ERZEUGT -->"))
n9 = sum(1 for s in L[k9:k10] if MARKE.match(s))
n10 = sum(1 for s in L[k10:k11] if MARKE.match(s))
ne = sum(1 for s in L[ea:ee + 1] if MARKE.match(s))
print("Marken in Abschnitt 9: %d, in Abschnitt 10: %d, im ERZEUGT-Block: %d (Soll je 0)" % (n9, n10, ne))
if n9 or n10 or ne:
    fehler.append("Abschnitt 9/10/ERZEUGT")

print("## Abschnitt 10 und ERZEUGT-Block gegen 0b (bytegleich)")
a10 = "\n".join(L[k10:k11]) + "\n"
erz = "\n".join(L[ea:ee + 1]) + "\n"
v10 = open(BL + "0b_abschnitt10_vorher.txt", encoding="utf-8").read()
verz = open(BL + "0b_erzeugt_vorher.txt", encoding="utf-8").read()
print("Abschnitt 10: Z. %d-%d, gleich 0b: %s" % (k10 + 1, k11, "ja" if a10 == v10 else "NEIN"))
print("ERZEUGT-Block: Z. %d-%d, gleich 0b: %s" % (ea + 1, ee + 1, "ja" if erz == verz else "NEIN"))
if a10 != v10 or erz != verz:
    fehler.append("Abschnitt 10/ERZEUGT")
if fehler:
    print("ABWEICHUNG:", fehler)
    sys.exit(1)
print("rc 0: alles wie Anhang A")

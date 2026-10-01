#!/usr/bin/env python3
"""Prueft die Markentabelle TB-126 gegen das Register am Stand 41864d4.

Aufruf:  python3 pruefe_markentabelle_tb126.py <markentabelle_tb126.md> <repo-wurzel>
Liest den JSON-Block der Markentabelle (zwischen den Zeilen 'DATEN-ANFANG' und 'DATEN-ENDE'),
zaehlt jeden Anker mit str.count ueber den ganzen Registertext, prueft Ankerzeile und
Einfuegestelle, simuliert das Einsetzen (Marken + angehaengte Bloecke 47-49) und zaehlt erneut.
rc 0 = alles wie angegeben, rc 1 = Abweichung.
"""
import hashlib, json, re, sys

md, repo = sys.argv[1], sys.argv[2].rstrip("/") + "/"
roh = open(md, encoding="utf-8").read()
daten = json.loads(roh.split("DATEN-ANFANG\n", 1)[1].split("\nDATEN-ENDE", 1)[0])
reg = open(repo + "docs/VORREGISTRIERUNG_neuselektion.md", encoding="utf-8").read()
L = reg.split("\n")
fehler = []
def f(x): fehler.append(x)

if hashlib.md5(reg.encode()).hexdigest() != "c8a32c0f0037c6c65bd08aae6be5a7c1": f("Register-md5 weicht ab")
if len(reg.splitlines()) != 10347: f("Register-Zeilenzahl weicht ab")
a10 = next(i for i, s in enumerate(L, 1) if s.startswith("## 10."))
a11 = next(i for i, s in enumerate(L, 1) if s.startswith("## 11."))
ea = next(i for i, s in enumerate(L, 1) if s.startswith("<!-- ERZEUGT:"))
ee = next(i for i, s in enumerate(L, 1) if s.startswith("<!-- ENDE ERZEUGT -->"))

marken = daten["marken"]
for m in marken:
    n = reg.count(m["anker"])
    if n != 1: f(f"Nr {m['nr']}: Anker {m['anker']!r} zaehlt {n}")
    if not L[m["ankerzeile"] - 1].startswith(m["anker"]): f(f"Nr {m['nr']}: Anker beginnt nicht Zeile {m['ankerzeile']}")
    if not L[m["nach"] - 1].startswith(m["anfang40"]): f(f"Nr {m['nr']}: Zeile {m['nach']} beginnt nicht wie angegeben")
    if a10 <= m["nach"] < a11: f(f"Nr {m['nr']}: Einfuegestelle in Abschnitt 10")
    if ea <= m["nach"] < ee: f(f"Nr {m['nr']}: Einfuegestelle im ERZEUGT-Block")
    if L[m["nach"] - 1].startswith(">") and L[m["nach"]].startswith(">"): f(f"Nr {m['nr']}: mitten im Zitat")
    if L[m["nach"] - 1].startswith("|") and L[m["nach"]].startswith("|"): f(f"Nr {m['nr']}: mitten in Tabelle")
    if not re.match(r"^> ⭐ \*\*.+ (PRÄZISIERT|ERGÄNZT|BERICHTIGT)( \(Verweis\))? durch .+\*\* \(.+, TB-126, ⟨DATUM⟩\)\.$", m["m1"]):
        f(f"Nr {m['nr']}: Markenzeile 1 nicht in der Form")
    if m["m2"] != "> Eintrag und Stand oben bleiben zeichengleich.": f(f"Nr {m['nr']}: Markenzeile 2")
# Reihenfolge: nach Einfuegestelle, dann R aufsteigend (B3 ohne R zuletzt)
schl = [(m["nach"], m["R"] or 999) for m in marken]
if schl != sorted(schl): f("Reihenfolge nicht nach Einfuegestelle/R")
if [m["nr"] for m in marken] != list(range(1, len(marken) + 1)): f("Nummern nicht fortlaufend")

# Simulation: Marken von unten nach oben einsetzen, Bloecke 47-49 anhaengen
neu = L[:]
for m in sorted(marken, key=lambda m: (m["nach"], m["R"] or 999, m["nr"]), reverse=True):
    neu[m["nach"]:m["nach"]] = ["", m["m1"], m["m2"]]
QUELLEN = {"27c": ("FABLE_ANTWORT_2026-09-27c_leiter_lesarten_und_wachen.md", 161, 209),
           "29b": ("FABLE_ANTWORT_2026-09-29b_sammlung_erzeuger_kalter_leser.md", 190, 267),
           "30a": ("FABLE_ANTWORT_2026-09-30a_vorgepruefte_fragen_e2.md", 25, 32)}
bl = {}
for q, (dat, a, b) in QUELLEN.items():
    z = open(repo + "docs/projektfuehrung/" + dat, encoding="utf-8").read().split("\n")
    cur = None
    for i in range(a, b + 1):
        s = z[i - 1]
        mm = re.match(r"^(\*\*)?R(\d+) — ", s)
        if mm: cur = int(mm.group(2)); bl[cur] = [s]; continue
        if cur is not None:
            bl[cur].append(s)
            if s.startswith("Quelle des Grundes:") or s.startswith("*Quelle des Grundes:*"): cur = None
if sorted(bl) != list(range(18, 56)): f("Schnitt ergibt nicht R18-R55")
anhang = []
for u in daten["ueberschriften"]:
    anhang += ["", u["zeile"], ""] + ["> " + z for z in bl[u["R"]]] + ["", "**Kette:** …"]
    if u["R"] == 48:
        r54 = daten["r54_unter_48_16"]
        anhang[-1:-1] = ["", r54["m1"], r54["m2"], ""]
sim = "\n".join(neu + anhang)
for m in marken:
    n = sim.count(m["anker"])
    if n != 1: f(f"Nr {m['nr']}: Anker nach Simulation {n}")
n54 = sim.count(daten["r54_unter_48_16"]["anker"])
if n54 != 1: f(f"R54-Anker (48.16) nach Simulation {n54}")
zz = [u["zeile"] for u in daten["ueberschriften"]]
if len(set(zz)) != 38 or any(sim.count(z) != 1 for z in zz): f("Ueberschriften nicht eindeutig")
if any(len(z) > 120 for z in zz): f("Ueberschrift laenger als 120 Zeichen")
# Altzeilen unveraendert und in Reihenfolge (append-only)
it = iter(neu)
if not all(any(x == y for y in it) for x in L): f("alte Zeilen nicht in Reihenfolge erhalten")

je = {}
for m in marken:
    k = next((int(re.match(r"## (\d+)\.", L[i - 1]).group(1)) for i in range(m["nach"], 0, -1) if re.match(r"## \d+\.", L[i - 1])), -1)
    je[k] = je.get(k, 0) + 1
print("Marken am alten Ort:", len(marken), "+ 1 unter 48.16 =", len(marken) + 1)
print("je Abschnitt:", ", ".join(f"{'Kopf' if k < 0 else k}: {v}" for k, v in sorted(je.items())))
print("Anker mit Zahl 1 (Original):", sum(reg.count(m["anker"]) == 1 for m in marken), "von", len(marken))
print("Anker mit Zahl 1 (nach Simulation):", sum(sim.count(m["anker"]) == 1 for m in marken), "von", len(marken))
print("Ueberschriften:", len(zz), "max. Laenge", max(len(z) for z in zz))
if fehler:
    print("ABWEICHUNG:"); [print("  -", x) for x in fehler]; sys.exit(1)
print("rc 0: alles wie angegeben")

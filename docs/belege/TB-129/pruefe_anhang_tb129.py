#!/usr/bin/env python3
"""Prueft Anhang A von TB-129 gegen das Register am Stand db108a6 und die Fundstellen fuer 51.8.

Aufruf:  python3 pruefe_anhang_tb129.py <MAC_TB-129_register_fable_01a.md> <repo-wurzel>
Liest den JSON-Block des Auftrags (zwischen den Zeilen 'DATEN-ANFANG' und 'DATEN-ENDE'), zaehlt jeden
Anker mit str.count ueber den ganzen Registertext, prueft Ankerzeile und Einfuegestelle, schneidet die
Quelle nach der Schnittregel, simuliert das Einsetzen (Marken + angehaengter Abschnitt 51) und zaehlt
erneut; prueft Fundstellen, Zaehlungen und den Kalender. Die Git-Tatsachen prueft die Sitzung mit git.
rc 0 = alles wie angegeben, rc 1 = Abweichung.
"""
import csv, datetime, hashlib, json, re, sys

md, repo = sys.argv[1], sys.argv[2].rstrip("/") + "/"
roh = open(md, encoding="utf-8").read()
daten = json.loads(roh.split("DATEN-ANFANG\n", 1)[1].split("\nDATEN-ENDE", 1)[0])
reg = open(repo + daten["register"], encoding="utf-8").read()
L = reg.split("\n")
fehler = []
def f(x): fehler.append(x)

if hashlib.sha256(reg.encode()).hexdigest() != daten["register_sha256"]: f("Register-sha256 weicht ab")
if len(reg.splitlines()) != daten["register_zeilen"]: f("Register-Zeilenzahl weicht ab")
a9 = next(i for i, s in enumerate(L, 1) if s.startswith("## 9."))
a11 = next(i for i, s in enumerate(L, 1) if s.startswith("## 11."))
ea = next(i for i, s in enumerate(L, 1) if s.startswith("<!-- ERZEUGT:"))
ee = next(i for i, s in enumerate(L, 1) if s.startswith("<!-- ENDE ERZEUGT -->"))
if reg.count("## 51.") != 0: f("## 51. ist schon vergeben")
if any(s.startswith("> R56 — ") for s in L): f("R56 steht schon im Register")

FORM = re.compile(r"^> ⭐ \*\*.+ (PRÄZISIERT|ERGÄNZT|BERICHTIGT) durch .+\*\* \(.+, TB-129, ⟨DATUM⟩\)\.$")
marken = daten["marken"]
for m in marken:
    n = reg.count(m["anker"])
    if n != 1: f(f"Nr {m['nr']}: Anker {m['anker']!r} zaehlt {n}")
    if not L[m["ankerzeile"] - 1].startswith(m["anker"]): f(f"Nr {m['nr']}: Anker beginnt nicht Zeile {m['ankerzeile']}")
    if not L[m["nach"] - 1].startswith(m["anfang40"]): f(f"Nr {m['nr']}: Zeile {m['nach']} beginnt nicht wie angegeben")
    if a9 <= m["nach"] < a11: f(f"Nr {m['nr']}: Einfuegestelle in Abschnitt 9 oder 10")
    if ea <= m["nach"] < ee: f(f"Nr {m['nr']}: Einfuegestelle im ERZEUGT-Block")
    if L[m["nach"] - 1].startswith(">") and L[m["nach"]].startswith(">"): f(f"Nr {m['nr']}: mitten im Zitat")
    if L[m["nach"] - 1].startswith("|") and L[m["nach"]].startswith("|"): f(f"Nr {m['nr']}: mitten in Tabelle")
    if L[m["nach"]] != "": f(f"Nr {m['nr']}: nach der Einfuegestelle steht keine Leerzeile")
    if not FORM.match(m["m1"]): f(f"Nr {m['nr']}: Markenzeile 1 nicht in der Form")
    if m["m2"] != "> Eintrag und Stand oben bleiben zeichengleich.": f(f"Nr {m['nr']}: Markenzeile 2")
schl = [(m["nach"], m["R"]) for m in marken]
if schl != sorted(schl): f("Reihenfolge nicht nach Einfuegestelle/R")
if [m["nr"] for m in marken] != list(range(1, len(marken) + 1)): f("Nummern nicht fortlaufend")

# Quelle schneiden
q = daten["quelle"]
qroh = open(repo + q["pfad"], "rb").read()
if hashlib.md5(qroh).hexdigest() != q["md5"]: f("Quelle: md5 weicht ab")
if len(qroh) != q["bytes"]: f("Quelle: Bytes weichen ab")
z = qroh.decode("utf-8").split("\n")
bl, cur = {}, None
for i in range(q["von"], q["bis"] + 1):
    s = z[i - 1]
    mm = re.match(r"^R(\d+) — ", s)
    if mm: cur = int(mm.group(1)); bl[cur] = [s]; continue
    if cur is not None:
        bl[cur].append(s)
        if s.startswith("Quelle des Grundes:"): cur = None
if sorted(bl) != list(range(56, 63)): f("Schnitt ergibt nicht R56-R62")
if any(len(v) != 2 or not v[1].endswith("Kein Ergebnis.") for v in bl.values()): f("ein Block hat nicht zwei Zeilen")

# Ueberschriften: Bezug = Anfang des Blocks bis zum ersten Punkt nach dem Bezug
for u in daten["ueberschriften"]:
    kern = u["zeile"].split(" ", 2)[2]                      # "R56 — ..."
    if not bl[u["R"]][0].startswith(kern + "."): f(f"{u['xn']}: Ueberschrift ist nicht der Blockanfang")
    if not u["kette"].startswith("**Kette:** "): f(f"{u['xn']}: Kette nicht in der Form")

# Simulation: Marken von unten nach oben einsetzen, Abschnitt 51 anhaengen
neu = L[:]
for m in sorted(marken, key=lambda m: (m["nach"], m["R"], m["nr"]), reverse=True):
    neu[m["nach"]:m["nach"]] = ["", m["m1"], m["m2"]]
anhang = ["## 51. Fable 01a — Registerblock R56–R62 (TB-129)", ""]
for u in daten["ueberschriften"]:
    anhang += [u["zeile"], ""] + ["> " + s for s in bl[u["R"]]] + ["", u["kette"], ""]
sim = "\n".join(neu[:-1] + [""] + anhang)
for m in marken:
    n = sim.count(m["anker"])
    if n != 1: f(f"Nr {m['nr']}: Anker nach Simulation {n}")
zz = [u["zeile"] for u in daten["ueberschriften"]]
if len(set(zz)) != 7 or any(sim.count(x) != 1 for x in zz): f("Ueberschriften nicht eindeutig")
if any(len(x) > 120 for x in zz): f("Ueberschrift laenger als 120 Zeichen")
it = iter(neu)
if not all(any(x == y for y in it) for x in L): f("alte Zeilen nicht in Reihenfolge erhalten")

# Fundstellen, Zaehlungen, Kalender
for d, znr, teil in daten["fundstellen"]:
    zl = open(repo + d, encoding="utf-8").read().split("\n")
    if znr > len(zl) or teil not in zl[znr - 1]: f(f"Fundstelle {d}:{znr} enthaelt nicht {teil!r}")
for d, muster, soll in daten["zaehlungen"]:
    ist = len(re.findall(muster, open(repo + d, encoding="utf-8").read(), re.M))
    if ist != soll: f(f"Zaehlung {d} /{muster}/: {ist} statt {soll}")
k = daten["kalender"]
for d in k["dateien"]:
    tage = [r[0][:10] for r in csv.reader(open(repo + d, encoding="utf-8"))][1:]
    bis = [t for t in tage if t <= "2018-01-31"]
    tag = datetime.date.fromisoformat
    ist = {"erster": tage[0], "balken_bis_2017-12-31": sum(t <= "2017-12-31" for t in tage),
           "index_149": tage[149], "index_150": tage[150],
           "tage_januar_2018": sum("2018-01-01" <= t <= "2018-01-31" for t in tage),
           "luecken_bis_2018-01-31": sum((tag(b) - tag(a)).days != 1 for a, b in zip(bis, bis[1:])),
           "doppelte_bis_2018-01-31": len(bis) - len(set(bis))}
    if ist != k["soll"]: f(f"Kalender {d}: {ist}")

je = {}
for m in marken:
    kk = next(int(re.match(r"## (\d+)\.", L[i - 1]).group(1)) for i in range(m["nach"], 0, -1) if re.match(r"## \d+\.", L[i - 1]))
    je[kk] = je.get(kk, 0) + 1
print("Marken:", len(marken), "an", len({m["nach"] for m in marken}), "Einfuegestellen")
print("je Abschnitt:", ", ".join(f"{a}: {v}" for a, v in sorted(je.items())))
print("Anker mit Zahl 1 (Original):", sum(reg.count(m["anker"]) == 1 for m in marken), "von", len(marken))
print("Anker mit Zahl 1 (nach Simulation):", sum(sim.count(m["anker"]) == 1 for m in marken), "von", len(marken))
print("Bloecke:", len(bl), "| Ueberschriften:", len(zz), "max. Laenge", max(len(x) for x in zz))
print("Fundstellen:", len(daten["fundstellen"]), "| Zaehlungen:", len(daten["zaehlungen"]), "| Kalender:", len(k["dateien"]), "Dateien")
print("Git-Tatsachen:", len(daten["git_tatsachen"]), "- von der Sitzung mit git zu pruefen")
if fehler:
    print("ABWEICHUNG:"); [print("  -", x) for x in fehler]; sys.exit(1)
print("rc 0: alles wie angegeben")

#!/usr/bin/env python3
"""Prueft Anhang A von TB-139 gegen das Register am Stand 9b7b060, die Quelle 07a und die Fundstellen fuer 55.7
und 55.8; auf Wunsch den Arbeitsbaum vor Schritt 0. Das Datum des Eintrags steht nicht im Auftrag: es kommt mit --datum.
Abgeleitet aus docs/belege/TB-136/0d_vorpruefung.py. Neu gegenueber TB-136: die drei Dateien der Fassung 06.10.a sind
von git verfolgt und im Commit dateien_frueher.commit dazugekommen; die drei Dateien 07.10.a sind ohne --arbeitsbaum
(also nach Schritt 0) von git verfolgt (R56 (b)); Platzhalter des Entwurfs in sechs Formen.

Aufruf (Python 3.9, nur Standardbibliothek; rein lesend):
  python3 pruefe_anhang_tb139.py <MAC_TB-139_register_fable_07a.md> <repo-wurzel> --datum TT.MM.JJJJ [Schalter]

  ohne Schalter      kein Platzhalter mehr im Auftrag (Freigabe eingesetzt), Register (sha256, Zeilen), Marken (Anker,
                     Einfuegestellen, Form), Quelle (md5, Schnittregel), Ueberschriften, Simulation des Einsetzens,
                     Dateien (md5; von git verfolgt; Commit der Fassung 06.10.a), Fundstellen, Zaehlungen. Das ist 0d.
  --arbeitsbaum      dazu: uncommittete Dateien genau wie im Daten-Block (0a, VOR dem Commit von Schritt 0).
                     Gemessen mit `git --no-optional-locks diff --name-only HEAD` und
                     `git --no-optional-locks ls-files --others --exclude-standard`.
  --datum TT.MM.JJJJ Pflicht. Das Datum des Eintrags; es ersetzt den Platzhalter ⟨DATUM⟩ in den Markenzeilen. Geprueft
                     wird die Form, keine Uhr. Jede Markenzeile 1 im Daten-Block traegt den Platzhalter genau einmal.
  --trockenlauf      NUR fuer den steuernden Chat vor der Sitzung; der Auftrag benutzt diesen Schalter nicht.
                     Uebergeht (a) Zaehlungen in BACKLOG*.md (Leseregel des Helfers),
                     (b) im Arbeitsbaum die Dateien, die erst mit dem Auftrag gelegt werden (Feld "spaeter"),
                     (c) die Platzhalter des Entwurfs, solange sie noch nicht ersetzt sind (auch in "fundstellen"
                         und in "arbeitsbaum.head"),
                     (d) die Pruefung, dass die drei Dateien 07.10.a von git verfolgt sind (vor Schritt 0 sind sie es nicht).
                     Jede Auslassung wird in der Ausgabe genannt.

rc 0 = alles wie angegeben, rc 1 = Abweichung, rc 2 = Aufruf unbrauchbar.
"""
import datetime
import glob
import hashlib
import json
import re
import subprocess
import sys

argv = sys.argv[1:]
schalter = {"--arbeitsbaum": False, "--trockenlauf": False}
datum = None
rest = []
i = 0
while i < len(argv):
    if argv[i] in schalter:
        schalter[argv[i]] = True
    elif argv[i] == "--datum":
        i += 1
        datum = argv[i] if i < len(argv) else None
        if datum is None:
            print("--datum braucht TT.MM.JJJJ"); sys.exit(2)
    elif argv[i].startswith("--"):
        print("unbekannter Schalter", argv[i]); sys.exit(2)
    else:
        rest.append(argv[i])
    i += 1
if len(rest) != 2:
    print(__doc__); sys.exit(2)
md, repo = rest[0], rest[1].rstrip("/") + "/"
TROCKEN = schalter["--trockenlauf"]
roh = open(md, encoding="utf-8").read()
daten = json.loads(roh.split("DATEN-ANFANG\n", 1)[1].split("\nDATEN-ENDE", 1)[0])
fehler = []
def f(x): fehler.append(x)
def lies(d): return open(repo + d, encoding="utf-8").read()
def ende():
    if fehler:
        print("ABWEICHUNG:"); [print("  -", x) for x in fehler]; sys.exit(1)
    print("rc 0: alles wie angegeben"); sys.exit(0)

# ---------------------------------------------------------------- Datum (vom Aufruf, nicht aus dem Auftrag)
try:
    if datum is None or datetime.datetime.strptime(datum, "%d.%m.%Y").strftime("%d.%m.%Y") != datum: raise ValueError
except ValueError:
    print("--datum TT.MM.JJJJ fehlt oder ist kein Datum:", datum); sys.exit(2)
print("Datum des Eintrags: %s (aus --datum)" % datum)
for m in daten["marken"]:
    if m["m1"].count("⟨DATUM⟩") != 1: f("Nr %d: Markenzeile 1 traegt den Platzhalter fuer das Datum nicht genau einmal" % m["nr"])
    m["m1"] = m["m1"].replace("⟨DATUM⟩", datum)
AUF, ZU = "<" + "<", ">" + ">"                  # zusammengesetzt, damit dieses Skript keinen Platzhalter in den Auftrag traegt
FORMEN = ("HEAD", "FREIGABE", "ENTSCHEID", "OFFEN", "BEFUNDE-07a", "BEFUNDE-07a-KURZ")
platz = {x: roh.count(AUF + x + ":") + roh.count(AUF + x + ZU) for x in FORMEN}
def offen(x): return isinstance(x, str) and AUF in x
if sum(platz.values()):
    text = ", ".join("%s %d" % (x, platz[x]) for x in FORMEN)
    if TROCKEN: print("Trockenlauf: im Auftrag stehen noch Platzhalter: " + text)
    else: f("im Auftrag stehen noch Platzhalter (%s); der Platzhalter FREIGABE ist die Freigabe des Betreibers" % text)

# ---------------------------------------------------------------- Register, Marken
A = daten["abschnitt"]
reg = lies(daten["register"])
L = reg.split("\n")
if hashlib.sha256(reg.encode()).hexdigest() != daten["register_sha256"]: f("Register-sha256 weicht ab")
if len(reg.splitlines()) != daten["register_zeilen"]: f("Register-Zeilenzahl weicht ab")
a9 = next(i for i, s in enumerate(L, 1) if s.startswith("## 9."))
a11 = next(i for i, s in enumerate(L, 1) if s.startswith("## 11."))
ea = next(i for i, s in enumerate(L, 1) if s.startswith("<!-- ERZEUGT:"))
ee = next(i for i, s in enumerate(L, 1) if s.startswith("<!-- ENDE ERZEUGT -->"))
ueb = daten["ueberschriften"]
R1, R2 = ueb[0]["R"], ueb[-1]["R"]
if reg.count("## %d." % A) != 0: f("## %d. ist schon vergeben" % A)
if any(s.startswith("> R%d — " % R1) for s in L): f("R%d steht schon im Register" % R1)

FORM = re.compile(r"^> ⭐ \*\*.+ (PRÄZISIERT|ERGÄNZT|BERICHTIGT) durch R(\d+) \(%d\.(\d+)\).*\*\* \(Fable 07a R(\d+)(, .+)?, TB-139, %s\)\.$"
                  % (A, re.escape(datum)))
M2 = "> Eintrag und Stand oben bleiben zeichengleich."
marken = daten["marken"]
if len(marken) != daten["marken_zahl"]: f("Zahl der Marken ist nicht %d" % daten["marken_zahl"])
for m in marken:
    n = reg.count(m["anker"])
    if n != 1: f("Nr %d: Anker %r zaehlt %d" % (m["nr"], m["anker"], n))
    if not L[m["ankerzeile"] - 1].startswith(m["anker"]): f("Nr %d: Anker beginnt nicht Zeile %d" % (m["nr"], m["ankerzeile"]))
    if not L[m["nach"] - 1].startswith(m["anfang40"]): f("Nr %d: Zeile %d beginnt nicht wie angegeben" % (m["nr"], m["nach"]))
    if not m["nach"] > m["ankerzeile"]: f("Nr %d: Einfuegestelle liegt nicht nach dem Anker" % m["nr"])
    if a9 <= m["nach"] < a11: f("Nr %d: Einfuegestelle in Abschnitt 9 oder 10" % m["nr"])
    if ea <= m["nach"] <= ee: f("Nr %d: Einfuegestelle im ERZEUGT-Block" % m["nr"])
    if L[m["nach"] - 1].startswith(">") and L[m["nach"]].startswith(">"): f("Nr %d: mitten im Zitat" % m["nr"])
    if L[m["nach"] - 1].startswith("|") and L[m["nach"]].startswith("|"): f("Nr %d: mitten in Tabelle" % m["nr"])
    if L[m["nach"]] != "": f("Nr %d: nach der Einfuegestelle steht keine Leerzeile" % m["nr"])
    if any(re.match(r"^#{2,3} ", L[i - 1]) for i in range(m["ankerzeile"] + 1, m["nach"] + 1)) and not m["anker"].startswith("## "):
        f("Nr %d: zwischen Anker und Einfuegestelle steht eine Ueberschrift" % m["nr"])
    mm = FORM.match(m["m1"])
    if not mm: f("Nr %d: Markenzeile 1 nicht in der Form" % m["nr"])
    elif not (int(mm.group(2)) == m["R"] == int(mm.group(4)) and int(mm.group(3)) == m["R"] - R1 + 1):
        f("Nr %d: Blocknummer, Unterabschnitt und Klammer passen nicht zusammen" % m["nr"])
    if m["m2"] != M2: f("Nr %d: Markenzeile 2" % m["nr"])
    if m["m1"] in L: f("Nr %d: die Marke steht schon im Register" % m["nr"])
schl = [(m["nach"], m["R"], m["nr"]) for m in marken]
if schl != sorted(schl): f("Reihenfolge nicht nach Einfuegestelle/R")
if [m["nr"] for m in marken] != list(range(1, len(marken) + 1)): f("Nummern nicht fortlaufend")
if len(set(m["m1"] for m in marken)) != len(marken): f("eine Markenzeile kommt doppelt vor")

# ---------------------------------------------------------------- Quelle schneiden
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
    elif s.strip() != "": f("Quelle: Zeile %d steht ausserhalb eines Blocks" % i)
if sorted(bl) != list(range(R1, R2 + 1)): f("Schnitt ergibt nicht R%d-R%d" % (R1, R2))
if any(len(v) != 2 or not v[1].endswith("Kein Ergebnis.") for v in bl.values()): f("ein Block hat nicht zwei Zeilen")
if z[q["von"] - 2] != "```" or z[q["bis"]] != "```": f("Quelle: der Codezaun steht nicht direkt vor und nach den Bloecken")

# Ueberschriften: Bezug = Anfang des Blocks bis zum Satzpunkt nach dem Bezug; am Ende gekuerzt nur mit '…'
for n, u in enumerate(ueb, 1):
    if not u["zeile"].startswith("### %d.%d R%d — " % (A, n, u["R"])): f("%s: Ueberschrift beginnt nicht mit Nummer und Block" % u["xn"])
    kern = u["zeile"].split(" ", 2)[2]                      # "R<n> — ..."
    anfang = bl.get(u["R"], [""])[0]
    if kern.endswith("…"):
        if not anfang.startswith(kern[:-1]) or anfang[len(kern) - 1:len(kern)].isalnum() or kern[-2] == " ":
            f("%s: gekuerzte Ueberschrift ist nicht der Blockanfang bis zu einer Wortgrenze" % u["xn"])
    elif not anfang.startswith(kern + "."): f("%s: Ueberschrift ist nicht der Blockanfang" % u["xn"])
    if not u["kette"].startswith("**Kette:** "): f("%s: Kette nicht in der Form" % u["xn"])
    orte = [m["stelle"] for m in marken if m["R"] == u["R"]]
    if u["marken_zahl"] != len(orte): f("%s: Kette nennt %d Marken, Tabelle 2 hat %d" % (u["xn"], u["marken_zahl"], len(orte)))

# ---------------------------------------------------------------- Simulation: Marken einsetzen, Abschnitt anhaengen
neu = L[:]
for m in sorted(marken, key=lambda m: (m["nach"], m["R"], m["nr"]), reverse=True):
    neu[m["nach"]:m["nach"]] = ["", m["m1"], m["m2"]]
anhang = [daten["kopfzeile"], ""]
for u in ueb:
    anhang += [u["zeile"], ""] + ["> " + s for s in bl.get(u["R"], [])] + ["", u["kette"], ""]
sim = "\n".join(neu[:-1] + [""] + anhang)
for m in marken:
    n = sim.count(m["anker"])
    if n != 1: f("Nr %d: Anker nach Simulation %d" % (m["nr"], n))
zz = [u["zeile"] for u in ueb]
if len(set(zz)) != len(ueb) or any(sim.count(x) != 1 for x in zz): f("Ueberschriften nicht eindeutig")
if any(len(x) > 140 for x in zz): f("Ueberschrift laenger als 140 Zeichen")
it = iter(neu)
if not all(any(x == y for y in it) for x in L): f("alte Zeilen nicht in Reihenfolge erhalten")
if neu.count(M2) != L.count(M2) + len(marken): f("Zahl der Folgezeilen nach Simulation")

# ---------------------------------------------------------------- Dateien, Fundstellen, Zaehlungen
for d, md5, nbytes in daten["dateien"]:
    try:
        b = open(repo + d, "rb").read()
    except OSError:
        f("Datei fehlt: %s" % d); continue
    if hashlib.md5(b).hexdigest() != md5 or len(b) != nbytes: f("Datei %s: md5 oder Bytes weichen ab" % d)
def git(*a):
    r = subprocess.run(["git", "--no-optional-locks", "-C", repo] + list(a), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    if r.returncode != 0: f("git %s: rc %d" % (" ".join(a), r.returncode))
    return [x for x in r.stdout.split("\n") if x]
fr = daten["dateien_frueher"]
for d, md5, nbytes in fr["dateien"]:
    try:
        b = open(repo + d, "rb").read()
    except OSError:
        f("Datei fehlt: %s" % d); continue
    if hashlib.md5(b).hexdigest() != md5 or len(b) != nbytes: f("Datei %s: md5 oder Bytes weichen ab" % d)
    if git("ls-files", "--", d) != [d]: f("Datei %s ist nicht von git verfolgt (R56 (b))" % d)
    dazu = git("log", "--diff-filter=A", "--format=%h", "--abbrev=7", "--", d)
    if dazu != [fr["commit"]]: f("Datei %s: dazugekommen in %s, erwartet %s" % (d, dazu, fr["commit"]))
if TROCKEN: print("Trockenlauf: nicht geprueft, ob die drei Dateien 07.10.a von git verfolgt sind (vor Schritt 0)")
elif not schalter["--arbeitsbaum"]:
    for d, md5, nbytes in daten["dateien"]:
        if git("ls-files", "--", d) != [d]: f("Datei %s ist nach Schritt 0 nicht von git verfolgt (R56 (b))" % d)
cache = {}
def zeilen(d):
    if d not in cache: cache[d] = lies(d).split("\n")
    return cache[d]
fund_offen = 0
for d, znr, teil in daten["fundstellen"]:
    if offen(d) or offen(znr) or offen(teil) or not isinstance(znr, int):
        fund_offen += 1
        if not TROCKEN: f("Fundstelle %s traegt noch einen Platzhalter" % d)
        continue
    try:
        zl = zeilen(d)
    except OSError:
        f("Fundstelle %s: Datei fehlt" % d); continue
    if znr > len(zl) or teil not in zl[znr - 1]: f("Fundstelle %s:%d enthaelt nicht %r" % (d, znr, teil))
for d, teil, soll in daten["zeilen_mit"]:
    ist = [n for n, s in enumerate(zeilen(d), 1) if teil in s]
    if ist != soll: f("Zeilen mit %r in %s: %s statt %s" % (teil, d, ist, soll))
uebergangen = []
for d, muster, soll in daten["zaehlungen"]:
    if TROCKEN and "BACKLOG" in d:
        uebergangen.append("%s /%s/" % (d, muster)); continue
    ist = len(re.findall(muster, lies(d), re.M))
    if ist != soll: f("Zaehlung %s /%s/: %d statt %d" % (d, muster, ist, soll))
for gl, muster, summe, dateien in daten["glob_summen"]:
    pf = [p for p in sorted(glob.glob(repo + gl, recursive=True)) if "/ergebnisse/" not in p]
    if len(pf) < dateien: f("Glob %s: %d Dateien, mindestens %d erwartet" % (gl, len(pf), dateien))
    ist = sum(len(re.findall(muster, open(p, encoding="utf-8").read(), re.M)) for p in pf)
    if ist != summe: f("Summe %s /%s/: %d statt %d" % (gl, muster, ist, summe))
for gl, teil, dateien, mit in daten["glob_treffer"]:
    pf = sorted(glob.glob(repo + gl))
    ist = sum(teil in open(p, encoding="utf-8").read() for p in pf)
    if len(pf) != dateien or ist != mit: f("Glob %s: %d Dateien, %d mit %r, statt %d und %d" % (gl, len(pf), ist, teil, dateien, mit))
py = sorted(set(git("ls-files", "--", "*.py") + git("ls-files", "--others", "--exclude-standard", "--", "*.py")))
py = [p for p in py if "/ergebnisse/" not in "/" + p and not p.startswith("trading-env/")]
for muster, summe, dateien in daten["baum_summen"]:
    treffer = {}
    for p in py:
        try:
            n = len(re.findall(muster, open(repo + p, encoding="utf-8", errors="replace").read(), re.M))
        except OSError:
            continue
        if n: treffer[p] = n
    if sum(treffer.values()) != summe or len(treffer) != dateien:
        f("Baum /%s/: %d Treffer in %d Dateien statt %d in %d: %s" % (muster, sum(treffer.values()), len(treffer), summe, dateien, sorted(treffer)[:5]))

# ---------------------------------------------------------------- Arbeitsbaum (0a)
if schalter["--arbeitsbaum"]:
    ab = daten["arbeitsbaum"]
    kopf = git("rev-parse", "HEAD")
    if offen(ab["head"]):
        if TROCKEN: print("Trockenlauf: arbeitsbaum.head ist noch Platzhalter; HEAD ist %s" % (kopf[0][:7] if kopf else None))
        else: f("arbeitsbaum.head ist noch Platzhalter")
    elif not (kopf and kopf[0].startswith(ab["head"])): f("HEAD ist %s, erwartet %s" % (kopf[0][:7] if kopf else None, ab["head"]))
    for name, ist, soll in (("geaendert", git("diff", "--name-only", "HEAD"), ab["geaendert"]),
                            ("unverfolgt", git("ls-files", "--others", "--exclude-standard"), ab["unverfolgt"])):
        fehlt, mehr = sorted(set(soll) - set(ist)), sorted(set(ist) - set(soll))
        if TROCKEN:
            spaeter = [x for x in fehlt if x in ab["spaeter"]]
            fehlt = [x for x in fehlt if x not in ab["spaeter"]]
            if spaeter: print("Trockenlauf: noch nicht gelegt (%s): %s" % (name, ", ".join(spaeter)))
        if fehlt: f("Arbeitsbaum, %s, fehlt: %s" % (name, ", ".join(fehlt)))
        if mehr: f("Arbeitsbaum, %s, nicht erwartet: %s" % (name, ", ".join(mehr)))
        print("Arbeitsbaum %s: %d (Soll %d)" % (name, len(ist), len(soll)))
if uebergangen: print("Trockenlauf: Zaehlungen uebergangen: " + "; ".join(uebergangen))
if fund_offen and TROCKEN: print("Trockenlauf: Fundstellen mit Platzhalter uebergangen: %d" % fund_offen)

je = {}
for m in marken:
    kk = next(int(re.match(r"## (\d+)\.", L[i - 1]).group(1)) for i in range(m["nach"], 0, -1) if re.match(r"## \d+\.", L[i - 1]))
    je[kk] = je.get(kk, 0) + 1
print("Marken:", len(marken), "an", len({m["nach"] for m in marken}), "Einfuegestellen")
print("je Abschnitt:", ", ".join("%d: %d" % (a, v) for a, v in sorted(je.items())))
print("Anker mit Zahl 1 (Original):", sum(reg.count(m["anker"]) == 1 for m in marken), "von", len(marken))
print("Anker mit Zahl 1 (nach Simulation):", sum(sim.count(m["anker"]) == 1 for m in marken), "von", len(marken))
print("Bloecke:", len(bl), "| Ueberschriften:", len(zz), "max. Laenge", max(len(x) for x in zz), "| gekuerzt:", sum(x.endswith("…") for x in zz))
print("Dateien:", len(daten["dateien"]), "| Fundstellen:", len(daten["fundstellen"]), "| Zeilenlisten:", len(daten["zeilen_mit"]),
      "| Zaehlungen:", len(daten["zaehlungen"]) + len(daten["glob_summen"]) + len(daten["glob_treffer"]) + len(daten["baum_summen"]), "| *.py im Baum:", len(py))
ende()

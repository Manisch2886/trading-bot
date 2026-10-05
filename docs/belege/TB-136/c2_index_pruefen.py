#!/usr/bin/env python3
"""TB-136 C2/C3 Gegenprobe (Vorlage docs/belege/TB-132/c2_index_pruefen.py, dort nach TB-130 und Bauart TB-129): jede Angabe 'Z. <n>'
(auch Listen 'Z. a, b' und Bereiche 'Z. a–b' an jeder Zahl) in REGISTER_INDEX.md zeigt im Register am HEAD auf eine
Zeile mit einem Markenwort (ERSETZT, PRÄZISIERT, BERICHTIGT, ERGÄNZT, KORRIGIERT); die Zeile '*Frühere Vierteilung*'
(Teilgrenzen) ist ausgenommen. Dazu: die 14 Marken aus 01a stehen weiter mit ihrer Zeile in Abschnitt 6, die 12
Marken aus 02a in Abschnitt 7, die 21 Marken aus 02c in Abschnitt 8, die 15 Marken aus 04a in Abschnitt 9; der Block '### Indexzeilen aus Fable 04a'
traegt genau die zwei Zeilen aus C3 des Auftrags (am Commit S0); die fuenf Indexzeilen aus 01a tragen weiter den
Schluss aus TB-130; die Abschnittstabelle nennt 0-54 mit den Zeilen aus den Koepfen der Abschnittsdateien; die
Indexzeilen E-2 zaehlen weiter 6.
Aufruf: trading-env/bin/python3 docs/belege/TB-136/c2_index_pruefen.py <S0> <datum>
"""
import glob
import re
import subprocess
import sys

S0, DATUM = sys.argv[1], sys.argv[2]
I = open("docs/projektfuehrung/REGISTER_INDEX.md", encoding="utf-8").read()
L = open("docs/VORREGISTRIERUNG_neuselektion.md", encoding="utf-8").read().split("\n")
W = re.compile(r"ERSETZT|PRÄZISIERT|BERICHTIGT|ERGÄNZT|KORRIGIERT")
fehler = []
nummern = []
for s in I.split("\n"):
    if s.startswith("*Frühere Vierteilung*"):
        continue
    for m in re.finditer(r"Z\. (\d+(?:(?:, |–)\d+)*)", s):
        nummern += [int(x) for x in re.split(r", |–", m.group(1))]
ohne = [n for n in nummern if not W.search(L[n - 1])]
print("Zeilenangaben im Index: %d; mit Markenwort: %d" % (len(nummern), len(nummern) - len(ohne)))
for n in ohne:
    print("  ohne Markenwort: Z. %d: %s" % (n, L[n - 1][:100]))
if ohne:
    fehler.append("Zeilenangaben ohne Markenwort")
print("Indexzeilen E-2: %d (Soll 6)" % I.count("**Indexzeile E-2**"))
if I.count("**Indexzeile E-2**") != 6:
    fehler.append("Indexzeilen E-2")


def abschnitt(kopf):
    return I.split(kopf, 1)[1].split("\n---\n", 1)[0].split("\n## ", 1)[0]


for tb, kopf, datum, soll in (("TB-129", "## 6. Die Marken aus Fable 01a (TB-129)", "02.10.2026", 14),
                              ("TB-130", "## 7. Die Marken aus Fable 02a (TB-130)", "02.10.2026", 12),
                              ("TB-132", "## 8. Die Marken aus Fable 02c (TB-132)", "04.10.2026", 21),
                              ("TB-136", "## 9. Die Marken aus Fable 04a (TB-136)", DATUM, 15)):
    M = re.compile(r"^> ⭐ \*\*.*" + tb + r", " + re.escape(datum) + r"\)\.$")
    mz = [i + 1 for i, s in enumerate(L) if M.match(s)]
    a = abschnitt(kopf) if kopf in I else ""
    drin = [z for z in mz if ("| Z. %d |" % z) in a]
    print("Marken %s im Register: %d; mit ihrer Zeile in '%s': %d (Soll %d/%d)" % (tb, len(mz), kopf[3:], len(drin), soll, soll))
    if len(mz) != soll or len(drin) != soll:
        fehler.append("Marken %s" % tb)

# C3: zwei Zeilen aus dem Auftrag, zeichengleich, im Block unter Abschnitt 9
auf = subprocess.run(["git", "show", "%s:docs/auftraege/MAC_TB-136_register_fable_04a.md" % S0],
                     capture_output=True, text=True, check=True).stdout
c3 = auf.split("**C3. Indexzeilen aus Fable 04a (R77 (b) und (c)).**", 1)[1].split("\n```\n", 2)[1]
a8 = abschnitt("## 9. Die Marken aus Fable 04a (TB-136)") if "## 9. Die Marken aus Fable 04a (TB-136)" in I else ""
kb = "### Indexzeilen aus Fable 04a\n\n"
blk = a8.split(kb, 1)[1].rstrip("\n") if kb in a8 else ""
ok3 = blk == c3 and I.count("### Indexzeilen aus Fable 04a") == 1
print("C3: %d Zeilen aus dem Auftrag; im Block '### Indexzeilen aus Fable 04a' (Abschnitt 9) zeichengleich: %s"
      % (len(c3.split("\n")), "ja" if ok3 else "NEIN"))
if not ok3:
    fehler.append("C3")
n01a = I.count("Marke gesetzt in TB-130 (R65 (b), 52.3).")
print("Indexzeilen aus 01a mit dem Schluss aus TB-130: %d (Soll 5)" % n01a)
if n01a != 5:
    fehler.append("Indexzeilen 01a")

# Abschnittstabelle gegen die Koepfe
KOPF = re.compile(r"^# REGISTER-KOPIE Abschnitt (\d+) \(von 0–(\d+)\) — Register-Z\. (\d+)–(\d+) — ")
gut = 0
dateien = sorted(glob.glob("docs/projektfuehrung/register_kopie/REGISTER_KOPIE_ABSCHNITT_*.md"))
for d in dateien:
    k = KOPF.match(open(d, encoding="utf-8").readline())
    zeile = "| %s | `%s` | %s–%s |" % (k.group(1), d.rsplit("/", 1)[1], k.group(3), k.group(4))
    gut += I.count(zeile) == 1
print("Abschnittstabelle: %d/%d Zeilen gleich den Koepfen der Abschnittsdateien" % (gut, len(dateien)))
if gut != len(dateien) or len(dateien) != 55:
    fehler.append("Abschnittstabelle")
if fehler:
    print("ABWEICHUNG:", fehler)
    sys.exit(1)
print("rc 0")
